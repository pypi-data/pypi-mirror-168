import os, sys
import shutil
import matplotlib.pyplot as plt


def make_path_if_not_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)


def remove_make_path(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)


def copy_move_file(source, target):
    shutil.copy(source, target)

def draw_confusion_matrix(y_pred, y_true):
    # https: // vitalflux.com / accuracy - precision - recall - f1 - score - python - example /
    from sklearn.metrics import confusion_matrix
    from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

    conf_matrix = confusion_matrix(y_true=y_true, y_pred=y_pred)
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.matshow(conf_matrix, cmap=plt.cm.Oranges, alpha=0.3)
    for i in range(conf_matrix.shape[0]):
        for j in range(conf_matrix.shape[1]):
            ax.text(x=j, y=i, s=conf_matrix[i, j], va='center', ha='center', size='xx-large')

    plt.xlabel('Predictions', fontsize=18)
    plt.ylabel('Actuals', fontsize=18)
    plt.title('Confusion Matrix', fontsize=18)
    plt.savefig('confusion_matrix.png')
    print('Num. of Obj.: %.3d' % len(y_true))
    print('Num. Pos./ Num. Neg.: {}/{}'.format(y_true.count(1), y_true.count(0)))
    print('Precision: %.3f' % precision_score(y_true, y_pred))
    print('Recall: %.3f' % recall_score(y_true, y_pred))
    print('Accuracy: %.3f' % accuracy_score(y_true, y_pred))
    print('F1 Score: %.3f' % f1_score(y_true, y_pred))
