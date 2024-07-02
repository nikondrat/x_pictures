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
}
