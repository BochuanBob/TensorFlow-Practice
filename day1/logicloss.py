import tensorflow as tf
from numpy.random import RandomState
w1 = tf.Variable(tf.random_normal([2,1], stddev = 1, seed = 1))
batch_size = 8

# x = tf.constant([[0.7, 0.9]])
x = tf.placeholder(tf.float32, shape = (None, 2), name = "x-input")
y_ = tf.placeholder(tf.float32, shape = (None, 1), name = "y-input")

y = tf.matmul(x, w1)

loss_more = 1
loss_less = 1
loss = tf.reduce_mean(tf.where(tf.greater(y, y_), 
	(y - y_) * loss_more,
	(y_ - y) * loss_less))
train_step = tf.train.AdamOptimizer(0.001).minimize(loss)

rdm = RandomState(1)
dataset_size = 128
X = rdm.rand(dataset_size, 2)

Y = [[x1 + x2 + rdm.rand()/10.0 - 0.05] for (x1, x2) in X]
sess = tf.Session()

init_op = tf.global_variables_initializer()
sess.run(init_op)


STEPS = 5000
for i in range(STEPS):
	start = (i * batch_size) % dataset_size
	end = min(start+batch_size, dataset_size)
	sess.run(train_step, feed_dict = {x: X[start:end], y_: Y[start:end]})

print(sess.run(w1))

sess.close()
