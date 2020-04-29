from Model.database import DatasetLoader
from Model.translate import *
import os

def g():
    dataset = DatasetLoader().load()
    print(len(dataset))
    g2g_translator = Gen2GenBuilder().train(dataset)
    command = input()
    while command != "exit":
        print(" ".join(g2g_translator.evaluate(command.split())))
        command = input()

def t():
    dataset = [
        [("x", "var"), ("=", ""), ("y", "var")],
        [("y", "var"), ("=", ""), ("x", "var")],
        [("a", "var"), ("=", ""), ("b", "var")],
        [("b", "var"), ("=", ""), ("a", "var")],
        [("x", "var"), ("=", ""), ("1", "num")],
        [("y", "var"), ("=", ""), ("-5", "num")],
        [("a", "var"), ("=", ""), ("7.5", "num")],
        [("b", "var"), ("=", ""), ("-134.6", "num")],
    ]
    builder = POSTaggerBuilder()
    model = builder.train(dataset, "file")
    print(model.evaluate(["a", "=", "x"]))
    model = builder.load("file")
    print(model.evaluate(["a", "=", "x"]))


def train():
    dataset = (DatasetLoader().load(), [
        [("x", "var"), ("=", ""), ("y", "var")],
        [("y", "var"), ("=", ""), ("x", "var")],
        [("a", "var"), ("=", ""), ("b", "var")],
        [("b", "var"), ("=", ""), ("a", "var")],
        [("x", "var"), ("=", ""), ("1", "num")],
        [("y", "var"), ("=", ""), ("-5", "num")],
        [("a", "var"), ("=", ""), ("7.5", "num")],
        [("b", "var"), ("=", ""), ("-134.6", "num")],
    ])
    builder = TranslationModeBuilder()
    builder.train(dataset, os.path.join(os.path.split(os.getcwd())[0], "saved-files"))


def translate():
    builder = TranslationModeBuilder()
    model = builder.load(os.path.join(os.path.split(os.getcwd())[0], "saved-files"))
    cmd = input()
    while cmd != "exit":
        print(model.evaluate(cmd))
        cmd = input()


train()

