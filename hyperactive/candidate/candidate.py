# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

from ..search_space import SearchSpace
from ..model import Model
from ..init_position import InitSearchPosition


class Candidate:
    def __init__(self, nth_process, _core_):
        self.search_config = _core_.search_config
        self.memory = _core_.memory

        self._score_best = -1000
        self.pos_best = None

        self.model = None

        self.nth_process = nth_process

        model_nr = nth_process % _core_.n_models
        self.func_ = list(_core_.search_config.keys())[model_nr]
        self._space_ = SearchSpace(_core_, model_nr)

        self.func_name = str(self.func_).split(" ")[1]

        self._space_.create_searchspace()
        self._model_ = Model(self.func_, nth_process)

        self._init_ = InitSearchPosition(
            self._space_, self._model_, _core_.warm_start, _core_.scatter_init
        )

    def create_start_point(self, para):
        start_point = {}

        temp_dict = {}
        for para_key in para:
            temp_dict[para_key] = [para[para_key]]

        start_point[self.func_name] = temp_dict

        return start_point

    def _get_warm_start(self):
        para_best = self._space_.pos2para(self.pos_best)
        warm_start = self.create_start_point(para_best)

        return warm_start

    @property
    def score_best(self):
        return self._score_best

    @score_best.setter
    def score_best(self, value):
        self.model_best = self.model
        self._score_best = value

    def eval_pos(self, pos, X, y, force_eval=False):
        pos_str = pos.tostring()

        if pos_str in self._space_.memory and self.memory and not force_eval:
            return self._space_.memory[pos_str]
        else:
            para = self._space_.pos2para(pos)
            score, eval_time, self.model = self._model_.train_model(para, X, y)
            self._space_.memory[pos_str] = score

            return score
