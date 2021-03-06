import tensorflow as tf
import tensorflow_hub as hub

from copy_graph import copy_op_to_graph, copy_variable_to_graph, get_copied_op


def main():

    tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

    g1 = tf.Graph()
    g2 = tf.Graph()

    scope = 'finetune'

    with g1.as_default():
        embed = hub.Module(
            "https://tfhub.dev/google/universal-sentence-encoder/1", trainable=True)
        sess = tf.compat.v1.Session(graph=g1)
        with sess.as_default():
            # copy all variables
            variables = []
            for variable in tf.compat.v1.global_variables():
                new_variable = copy_variable_to_graph(
                    variable, g2, True, scope)
                variables.append(new_variable)
            # copy all ops
            for op in g1.get_operations():
                copy_op_to_graph(op, g2, variables, scope)
            # copy table initilization
            copy_op_to_graph(tf.compat.v1.tables_initializer(), g2, variables, scope)

    tf.compat.v1.reset_default_graph()

    with g2.as_default():
        sess = tf.compat.v1.Session(graph=g2)
        with sess.as_default():

            sess.run(tf.compat.v1.global_variables_initializer())
            sess.run(tf.compat.v1.get_default_graph().get_operation_by_name(
                'finetune/init_all_tables'))

            in_tensor = tf.compat.v1.get_default_graph().get_tensor_by_name(
                scope + '/module/fed_input_values:0')
            ou_tensor = tf.compat.v1.get_default_graph().get_tensor_by_name(
                scope + '/module/Encoder_en/hidden_layers/l2_normalize:0')

            for v in tf.compat.v1.trainable_variables():
                print(v.name, v)

            save_path = 'model/USE.ckpt'
            saver = tf.compat.v1.train.Saver()
            saver.save(sess, save_path)


if __name__ == '__main__':
    main()
