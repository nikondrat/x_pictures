import 'package:flutter/material.dart';
import 'package:mobx/mobx.dart';

part 'view.g.dart';

class GenerateViewStore extends _GenerateViewStore with _$GenerateViewStore {
  GenerateViewStore();
}

abstract class _GenerateViewStore with Store {
  @observable
  int selected = 0;

  @action
  void setSelected(int index) {
    selected = index;
  }

  @observable
  int selectedStyle = 0;

  @action
  void setSelectedStyle(int index) {
    selectedStyle = index;
  }

  @observable
  int selectedFormat = 0;

  @action
  void setSelectedFormat(int index) {
    selectedFormat = index;
  }

  TextEditingController controller = TextEditingController();

  void dispose() {
    controller.dispose();
  }
}
