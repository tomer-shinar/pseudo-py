from translateapp.dataset_manager import DataSetManager
from datetime import datetime
from Model.translate import TranslationModeBuilder

"""
handle the training in the background
"""


def main():
    builder = TranslationModeBuilder()
    while True:
        start = datetime.now()
        print("start:", start)
        dataset = (DataSetManager.load_g2g_dataset(), DataSetManager.load_pos_dataset())
        print("dataset:")
        print(dataset[0])
        print(dataset[1])
        builder.train(dataset, "saved_files")
        end = datetime.now()
        print("finished at:", end)
        print("total time:", end - start)


if __name__ == "__main__":
    main()
