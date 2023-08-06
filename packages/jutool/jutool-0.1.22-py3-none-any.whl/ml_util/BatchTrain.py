import abc
from sample_util.SampleSet import SampleSet
from ml_util.TrainableModelBase import TrainableModelBase


class BatchTrainable:

    def __init__(self, model: TrainableModelBase,
                 epochs=1000,
                 update_freq_perbatch=1,
                 model_save_freq_perbatch=1,
                 ):
        self._model = model
        self._epochs = epochs
        self._update_freq_per_batch = update_freq_perbatch
        self._model_save_freq_per_batch = model_save_freq_perbatch

    def train(self, sampleset: SampleSet):

        for epoch in range(self._epochs):
            batch_result_act_list = []
            batch_result_sample_list = []
            batch_index = 0
            batch_save_counter = 0
            batch_update_counter = 0
            for sample in sampleset:
                batch_index += 1
                batch_update_counter += 1
                batch_save_counter += 1

                call_result = self._model.call(sample, train_mode=True)
                batch_result_act_list.append(call_result)
                batch_result_sample_list.append(sample)

                if batch_save_counter == self._model_save_freq_per_batch:
                    self._model.save(f"{self._model.Name}_{batch_index}")
                    batch_save_counter = 0

                if batch_update_counter == self._update_freq_per_batch:
                    self._model.update_parameters(batch_result_act_list, batch_result_sample_list)
                    batch_result_act_list = []
                    batch_result_sample_list = []
                    batch_update_counter = 0

    def evaluation(self, sampleset: SampleSet):
        pass
