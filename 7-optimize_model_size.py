import tensorflow as tf

saved_model_dir = "./trained/models/latest-large2-model-1622504119"


converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir) # path to the SavedModel directory
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.target_spec.supported_types = [tf.float16]

tflite_model = converter.convert()

with open('./trained/models/large2-optimized.tflite', 'wb') as f:
  f.write(tflite_model)