import logging
from typing import List, Type, Dict, Optional

import tensorflow as tf
from keras import Model
from keras.layers import Permute
from tensorflow import keras

from keras_data_format_converter.modelconverter import ModelConverter, calculate_permute_values
from keras_data_format_converter.utils import configure_logger


def convert_channels_first_to_last(model: keras.Model,
                                   should_transform_inputs_and_outputs=False,
                                   custom_layers: Optional[Dict[str, Type[tf.keras.layers.Layer]]] = None,
                                   verbose: bool = False) \
        -> keras.Model:
    """
    Convert keras models from channels first to last

    :param custom_layers: dictionary of custom layers
    :type custom_layers: Optional[Dict[str, Type[tf.keras.layers.Layer]]]
    :param verbose: by default true, set to False to lower the logging level
    :type verbose: bool
    :param model: keras model to convert in channels first format
    :type model: tensorflow.keras.Model
    :return: converted keras model in channels last format
    :rtype: tensorflow.keras.Model
    """
    converted_model = _convert_channels(model, custom_layers, verbose)
    if should_transform_inputs_and_outputs:
        converted_model = _transform_inputs_and_outputs(converted_model)

    return converted_model


def _convert_channels(model: tf.keras.Model,
                      custom_layers: Optional[Dict[str, Type[tf.keras.layers.Layer]]], verbose: bool) \
        -> tf.keras.Model:
    # configure logger
    configure_logger(verbose)
    logger = logging.getLogger(__name__)

    if custom_layers is None:
        custom_layers = {}

    model_converter = ModelConverter(model, custom_layers)
    converted_model = model_converter.convert_model()
    return converted_model


def _transform_inputs_and_outputs(k_model: Model) -> Model:
    new_inputs = []
    new_old_inputs = []
    for k_input in k_model.inputs:
        new_input_shape = Permute(
            calculate_permute_values(k_input.shape, to_channel_first=False))(k_input).shape[1:]
        new_input_tensor = tf.keras.Input(new_input_shape)
        back_to_channel_first_perm_values = calculate_permute_values(new_input_tensor.shape, to_channel_first=True)
        permute_after = Permute(back_to_channel_first_perm_values)(new_input_tensor)
        new_inputs.append(new_input_tensor)
        new_old_inputs.append(permute_after)

    new_outputs = []
    new_old_outputs = k_model.call(new_old_inputs)
    if not isinstance(new_old_outputs, list):
        new_old_outputs = [new_old_outputs]
    for output in new_old_outputs:
        perm_values = calculate_permute_values(output.shape, to_channel_first=False)
        new_outputs.append(Permute(perm_values)(output))

    return Model(inputs=new_inputs, outputs=new_outputs)
