from __future__ import annotations
from aenum import Enum, IntEnum, extend_enum
from source.classes.BabelFish import BabelFish
import json
import os

fish = BabelFish(lang="en")

def tokenize(token):
    for search,replace in (
      ('(', ""),
      (')',""),
      ("'", ""),
      ('-'," "),
      ('/',""),
      ("\\","")
    ):
        token = token.replace(search, replace)
    tokens = token.split(" ")
    i = 0
    for check in tokens:
        if check.lower() == check:
            tokens[i] = ""
        i += 1
    return " ".join(tokens).replace(" ","")

class Toggle(IntEnum):
    Off = 0
    On = 1

    @classmethod
    def from_text(cls, text: str) -> Toggle:
        if text.lower() in {"off", "0", "false", "none", "null"}:
            return Toggle.Off
        else:
            return Toggle.On

class Choice(IntEnum):
    @classmethod
    def from_text(cls, text: str) -> Choice:
        for option in cls:
            if option.name == text.upper():
                return option
        raise KeyError(
          'KeyError: Could not find option "%s" for "%s", known options are %s' %
          (
            text,
            cls.__name__,
            ", ".join(option.name for option in cls)
          )
        )

def create_choice(option_name,option_vals):
  option = type(option_name,(Choice,),{})
  for name in option_vals:
    extend_enum(option,str(name).upper(),len(option))
  return option

def load_options(filepath):
    theseCompiled = {}
    with open(filepath) as widgetsDefn:
        filepath = filepath.split(os.sep)
        domain = filepath[3]
        key = filepath[4]
        theseOptions = json.load(widgetsDefn)
        for section in theseOptions:
            widgets = theseOptions[section]
            for widget in widgets:
                thisWidget = widgets[widget]
                if domain == "randomize":
                    domain = "randomizer"
                if key == "entrando":
                    key = "entrance"
                fish_key = domain + '.' + key + '.' + widget
                option_name = tokenize(fish.translate("gui","gui",fish_key,"en"))
                if thisWidget["type"] == "checkbox":
                    theseCompiled[option_name] = Toggle
                elif thisWidget["type"] == "selectbox":
                    option_vals = thisWidget["options"]
                    theseCompiled[option_name] = create_choice(option_name,option_vals)
    return theseCompiled


if __name__ == "__main__":
    import argparse

    compiledOptions = {}
    notebooks = {
      "randomize": [ "dungeon", "enemizer", "entrando", "gameoptions", "generation", "item", "multiworld" ]
    }
    for notebook in notebooks:
        for page in notebooks[notebook]:
            for filename in ["keysanity","checkboxes","widgets"]:
                defn = os.path.join("resources", "app", "gui", notebook, page, filename + ".json")
                if os.path.isfile(defn):
                    compiledOptions.update(load_options(defn))

    test = argparse.Namespace()
    test.logic = compiledOptions["LogicLevel"].from_text("nologic")
    test.mapshuffle = compiledOptions["Maps"].from_text("ON")
    try:
        test.logic = compiledOptions["LogicLevel"].from_text("overworldglitches")
    except KeyError as e:
        print(e)
    if test.mapshuffle:
        print("Map Shuffle is on")
    print(test)
    for option in compiledOptions:
        print("%s: %s" % (option, list(compiledOptions[option])))
