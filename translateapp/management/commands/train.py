import os

from django.core.management.base import BaseCommand

from Model.translate import TranslationModeBuilder
from datetime import datetime

from translateapp.dataset_manager import DataSetManager


class Command(BaseCommand):
    help = 'train the model non stop'

    def handle(self, *args, **kwargs):
        builder = TranslationModeBuilder()
        start = datetime.now()
        print("start:", start)
        dataset = (DataSetManager.load_g2g_dataset(), DataSetManager.load_pos_dataset())
        print("dataset:")
        print(dataset[0])
        print()
        print(dataset[1])
        builder.train(dataset, "saved-files")
        end = datetime.now()
        print("finished at:", end)
        print("total time:", end - start)
