import tensorflow as tf
import importlib
import random
from preprocess.data_utils import utter_preprocess, is_reach_goal

class Target_Chat():
    def __init__(self, agent):
        self.agent = agent
        self.start_utter = config_data._start_corpus
        with tf.Session(config=self.agent.gpu_config) as sess:
            self.agent.retrieve_init(sess)
            for i in range(10):
                print('--------Session {} --------'.format(i))
                self.chat(sess)

    def chat(self, sess):
        history = []
        history.append(random.sample(self.start_utter, 1)[0])
        target_kw = random.sample(config_data._keywords_candi[:100], 1)[0]
        self.agent.target = target_kw
        self.agent.score = 0.
        self.agent.reply_list = []
        print('START: ' + history[0])
        for i in range(config_data._max_turns):
            history.append(input('HUMAN: '))
            source = utter_preprocess(history, self.agent.data_config._max_seq_len)
            reply = self.agent.retrieve(source, sess)
            print('AGENT: ', reply)
            print('Keyword: {}, Similarity: {:.2f}'.format(self.agent.next_kw, self.agent.score))
            history.append(reply)
            if is_reach_goal(history[-2] + history[-1], target_kw):
                print('Successfully chat to the target \'{}\'.'.format(target_kw))
                return
        print('Failed by reaching the maximum turn, target: \'{}\'.'.format(target_kw))

if __name__ == '__main__':
    flags = tf.flags
    # supports kernel / matrix / neural / retrieval / retrieval-stg
    flags.DEFINE_string('agent', 'kernel', 'The agent type')
    FLAGS = flags.FLAGS

    config_data = importlib.import_module('config.data_config')
    config_model = importlib.import_module('config.' + FLAGS.agent)
    model = importlib.import_module('model.' + FLAGS.agent)
    predictor = model.Predictor(config_model, config_data, 'test')
    Target_Chat(predictor)