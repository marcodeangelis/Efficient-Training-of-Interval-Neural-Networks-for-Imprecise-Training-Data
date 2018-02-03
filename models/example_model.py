from base.base_model import BaseModel, create_saver
import tensorflow as tf


class ExampleModel(BaseModel):
    def __init__(self, config):
        super(ExampleModel, self).__init__(config)

        ExampleModel.build_model = create_saver(ExampleModel.build_model)

        self.build_model()

        if self.saver is None:
            print("SHIT")
        else:
            print("GOOD")

        exit(0)


    def build_model(self):



        self.is_training = tf.placeholder(tf.bool)

        self.x = tf.placeholder(tf.float32, shape=[None] + self.config.state_size)
        self.y = tf.placeholder(tf.float32, shape=[None, 10])

        # network_architecture
        d1 = tf.layers.dense(self.x, 512, activation=tf.nn.relu, name="densee2")
        d2 = tf.layers.dense(d1, 10)

        with tf.name_scope("loss"):
            self.cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=self.y, logits=d2))
            self.train_step = tf.train.AdamOptimizer(self.config.learning_rate).minimize(self.cross_entropy,
                                                                                         global_step=self.global_step_tensor)
            correct_prediction = tf.equal(tf.argmax(d2, 1), tf.argmax(self.y, 1))
            self.accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

        print("\n\nModel built\n\n")