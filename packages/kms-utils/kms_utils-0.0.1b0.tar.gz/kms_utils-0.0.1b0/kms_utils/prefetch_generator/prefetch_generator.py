from __future__ import annotations

from collections import OrderedDict
from itertools import cycle
import logging
from multiprocessing import Process, Queue
import queue
from threading import Thread
import time
from typing import Callable, Dict, Iterable, List, Optional, Tuple, Union


logger = logging.getLogger(__name__)


class PrefetchGeneratorUnit(Process):
    def __init__(self, iterable: Iterable, num_prefetch: int, gid: int, processing_func: Optional[Callable] = None):
        """Prefetch Generator
        
        Args:
            iterable (Iterable): 데이터
            # queue (Queue): 데이터 반환할 큐
            num_prefetch (int): prefetch 개수
            gid (int): generator id
            processing_func (Callable): (Optional) 데이터 처리 함수
        """
        Process.__init__(self)
        self.iterable = iterable
        self.queue = Queue(maxsize=num_prefetch)
        self.num_prefetch = num_prefetch
        self.gid = gid
        self.processing_func = processing_func
        self.daemon = True
        self.start()

    def run(self):
        try:
            for idx, item in enumerate(self.iterable):
                # processing_func가 있으면 processing_func(item) 반환
                # # 없으면 그냥 item 반환
                item = item if self.processing_func is None else self.processing_func(item)
                # queue에 num_prefetch만큼 데이터가 있으면 여기서 멈춰있음
                # put에 넣는 첫번째 인자는 데이터, 두번째 인자는 실패 여부
                # logger.info(F"empty: {self.queue.empty()}, full: {self.queue.full()}, size: {self.queue.qsize()}")
                self.queue.put((item, self.gid, idx, False))
        except Exception as e:
            self.queue.put((e, self.gid, idx, True))
        finally:
            self.queue.put((StopIteration, self.gid, idx, True))


class PrefetchGenerator(Thread):
    """데이터를 병렬로 처리하는 generator

    Args:
        iterator (Union[List, Tuple, Dict, str]): iterable 데이터. generator는 지원하지 않음
        num_prefetch (int): prefetch 개수
        num_workers (int): 최대 Process 수. num_prefetch보다 작은 경우 num_prefetch와 같은 값으로 변경됨
        ordered (bool): 데이터 순서를 유지할 것인지(기본값=True)
        processing_func (Callable): (Optional) 데이터 처리 함수

    Attributes:
        results (OrderedDict): 전처리가 끝난 데이터를 {index: item} 형태로 저장
            ordered=True 이면, index를 0부터 차례로 증가시키며 데이터를 꺼냄
            ordered=False 이면, 데이터 처리가 끝난 순서대로 데이터를 꺼냄
        _units (Dict[str, PrefetchGeneratorUnit]): gid(PrefetchGeneratorUnit의 번호)를 key로 가지는 dictionary
        _c (itertools.cycle): 데이터를 꺼낼 PrefetchGeneratorUnit의 index를 순차적으로 출력
        _next_idx (int): ordered=True 인 경우, 다음에 꺼내야할 데이터 index
        _continue (bool): PrefetchGeneratorUnit 작업이 모두 끝나면 False로 변함
        _pendding (bool): pendding=True이면 PrefetchGeneratorUnit에서 데이터를 꺼냄
        _stoped_generators (int): 데이터 처리가 끝난 PrefetchGeneratorUnit의 개수
    """
    def __init__(self, iterator: Union[Dict, List, Tuple], num_prefetch: int = 1, num_workers: int = 1, ordered: bool = True, processing_func: Optional[Callable] = None) -> None:
        Thread.__init__(self)
        self.results = OrderedDict()
        self.ordered = ordered
        self.num_workers = min(num_prefetch, num_workers)
        self.num_prefetch = num_prefetch
        self.processing_func = processing_func

        num_prefetch_each_workers = max(self.num_prefetch//num_workers + (1 if self.num_prefetch%num_workers != 0 else 0) -1, 1)
        self._units = self.make_generators(iterator, num_prefetch_each_workers)
        self._c = cycle(range(self.num_workers))
        self._next_idx = 0
        self._continue = True
        self._pendding = False
        self._stoped_generators = 0
        self.daemon = True
        self.start()

    def make_generators(self, iterator, num_prefetch_each_workers) -> Dict[int, PrefetchGeneratorUnit]:
        """self.num_workers만큼 PrefetchGeneratorUnit 생성
        
        여러 유닛에 데이터를 순차적으로 할당
        iterator = [1, 2, 3, 4], num_workers = 2 인 경우,
        '유닛1' [1, 3], '유닛2'에는 [2, 4]가 할당됨

        Args:
            iterator (Union[List, Tuple, Dict, str]): iterable 데이터. generator는 지원하지 않음
            num_prefetch_each_workers (int): 각각의 unit에서 prefetch할 데이터 개수
        
        Returns:
            (Dict[int, PrefetchGeneratorUnit]): gid(PrefetchGeneratorUnit의 번호)를 key로 가지는 dictionary
        """
        generators = {gid: PrefetchGeneratorUnit(iterator[gid::self.num_workers], num_prefetch_each_workers, gid, self.processing_func) for gid in range(self.num_workers)}
        return generators

    def run(self):
        """여러 PrefetchGeneratorUnit에서 데이터를 꺼냄
        
        유닛에서 데이터를 꺼내서 self.results에 저장
        """
        c = cycle(range(self.num_workers))
        while self._stoped_generators < self.num_workers:
            try:
                if self._pendding:
                    # item: 데이터
                    # gid: unit의 번호
                    # idx: unit 내부의 몇 번째 데이터인지
                    # err: 오류 여부. 오류가 아니면 False
                    item, gid, idx, err = self._units[next(c)].queue.get_nowait()

                    # 전체 데이터에서의 index 계산
                    total_idx = gid+idx*self.num_workers
                    if not err:
                        self.results[total_idx] = item
                    else:
                        if item is StopIteration:
                            # unit 하나가 종료됨
                            self._stoped_generators += 1
                            self._units[gid].terminate()
                        else:
                            logger.debug(f"StopIteration말고 다른 오류 발생 {e}", exc_info=True)
                            self._continue = False
                            raise item
                else:
                    # self._pendding=True가 될때까지, 즉 __next__가 수행될때까지 대기
                    # unit에서 데이터 처리는 정상적으로 수행되고 있음
                    time.sleep(0.01)
            except queue.Empty:
                # unit에서 꺼낼 데이터가 없음
                # 잠깐 대기
                time.sleep(0.01)
            except Exception as e:
                logger.debug(f"여기에 무슨 오류가 오는지 모름 {e}", exc_info=True)
                pass
        self._continue = False

    def __next__(self):
        while True:
            if not self.results and not self._continue:
                # results에서 꺼낼 데이터도 없고, unit도 모두 종료된 상태
                raise StopIteration
            if (self._next_idx in self.results if self.ordered else self.results):
                # self.ordered=True 이면, self.results에서 next_idx를 꺼내고
                # self.ordered=False 이면, popitem(False)로 가장 오래된 데이터부터 꺼냄
                item = self.results.pop(self._next_idx) if self.ordered else self.results.popitem(False)[1]
                self._pendding = False
                self._next_idx +=1
                return item
            else:
                # unit에서 데이터가 준비될때까지 대기
                self._pendding = True
                time.sleep(0.01) 
          
    def __iter__(self):
        return self
