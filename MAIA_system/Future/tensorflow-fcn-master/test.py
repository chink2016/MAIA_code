import tensorflow as tf
import fcn16_vgg
import loss

IMAGE_SIZE = 400
IMAGE_PIXELS = IMAGE_SIZE * IMAGE_SIZE
NUM_CLASSES = 4
batch_size = 10

with tf.Graph().as_default():
    images_placeholder = tf.placeholder(tf.float32, shape=(batch_size, IMAGE_PIXELS))
    labels_placeholder = tf.placeholder(tf.float32, shape=(batch_size, IMAGE_PIXELS))
    vgg_fcn = fcn16_vgg.FCN16VGG()
    with tf.name_scope("content_vgg"):
        vgg_fcn.build(images_placeholder, debug=True)
    myloss = loss(vgg_fcn.pred_up, labels_placeholder)