import coremltools
from keras.models import load_model

coreml_model = coremltools.converters.keras.convert('observed_cnn_epoch=100.h5',input_names = 'image'
,image_input_names = 'image',output_names='Prediction',class_labels = ["vehicle","bike","human"],)

coreml_model.save('./observed_cnn_epoch=100.mlmodel')
