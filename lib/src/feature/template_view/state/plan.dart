import 'package:flutter/material.dart';
import 'package:x_pictures/src/feature/template_view/enum/enum.dart';

class PlanState extends ChangeNotifier {
  bool _isSelected = false;
  List<bool> _isSelectedList = [false, false, false];
  Plan _currentPlan = Plan.notSelected;

  bool get isSelected => _isSelected;
  List<bool> get isSelectedList => _isSelectedList;
  Plan get currentPlan => _currentPlan;

  void changeCurrentPlan(Plan value){
    _currentPlan = value;
    notifyListeners();
  }

  void setTrueToIsSelectedList(int index)
  {
    _isSelectedList = _isSelectedList.map((element) => false).toList();
    _isSelectedList[index] = true;
    _isSelected = true;
    notifyListeners();
  }
}