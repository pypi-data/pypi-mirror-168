from ml_util.TrainableProcessModelBase import TrainableProcessModelBase
from sample_util.SampleSet import SampleSet
from code_util.log import process_status_bar


class BatchTrainable:

    def __init__(self, model: TrainableProcessModelBase,
                 epochs=1000,
                 update_freq_perbatch=1,
                 model_save_freq_perbatch=1,
                 ):
        self._model = model
        self._epochs = epochs
        self._update_freq_per_batch = update_freq_perbatch
        self._model_save_freq_per_batch = model_save_freq_perbatch

    def train(self, sampleset: SampleSet):

        ps_bar = process_status_bar()

        for epoch in ps_bar.iter_bar(range(self._epochs), key="epoch", max=self._epochs):
            batch_result_act_list = []
            batch_result_sample_list = []
            batch_index = 0
            batch_save_counter = 0
            batch_update_counter = 0
            for sample in ps_bar.iter_bar(sampleset, key="set_iter", max=sampleset.count()):
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
