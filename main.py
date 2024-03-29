import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

minst = input_data.read_data_sets('MNIST_data', one_hot=True)


# 预测精度函数
def add_layer(inputs, in_size, out_size, activation_function=None):
    Weights = tf.Variable(tf.random_normal([in_size, out_size]), name='w')
    biases = tf.Variable(tf.random_normal([1, out_size]), name='b')
    Wx_plus_b = tf.matmul(inputs, Weights) + biases
    if activation_function is None:
        outputs = Wx_plus_b
    else:
        outputs = activation_function(Wx_plus_b)
    return outputs


# 精度计算函数
def compute_accuracy(v_xs, v_ys):
    global prediction
    y_pre = sess.run(prediction, feed_dict={xs: v_xs})
    currect_prediction = tf.equal(tf.argmax(y_pre, 1), tf.argmax(v_ys, 1))
    accuracy = tf.reduce_mean(tf.cast(currect_prediction, tf.float32))
    result = sess.run(accuracy, feed_dict={xs: v_xs, ys: v_ys})
    return result


xs = tf.placeholder(tf.float32, [None, 784])
ys = tf.placeholder(tf.float32, [None, 10])
prediction = add_layer(xs, 784, 10, activation_function=tf.nn.softmax)
cross_entropy = tf.reduce_mean(-tf.reduce_sum(ys * tf.log(prediction), reduction_indices=[1]))
train_steps = tf.train.GradientDescentOptimizer(0.6).minimize(cross_entropy)

init = tf.initialize_all_variables()
sess = tf.Session()
sess.run(init)
for i in range(5000):
    batch_xs, batch_ys = minst.train.next_batch(256)
    sess.run(train_steps, feed_dict={xs: batch_xs, ys: batch_ys})
    if i % 100 == 0:
        print(compute_accuracy(minst.test.images, minst.test.labels))
