import 'package:mobx/mobx.dart';

part 'tools.g.dart';

class ToolsViewStore extends _ToolsViewStore with _$ToolsViewStore {
  ToolsViewStore();
}

abstract class _ToolsViewStore with Store {
  @observable
  double size = 40;

  @action
  void setSize(double value) => size = value;

  @observable
  int selectedTool = 0;

  @action
  void setSelectedTool(int value) => selectedTool = value;
}
