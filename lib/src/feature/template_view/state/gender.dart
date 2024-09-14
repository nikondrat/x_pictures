import 'package:flutter/material.dart';
import 'package:x_pictures/src/feature/template_view/enum/enum.dart';

class GenderState extends ChangeNotifier {
  bool _isSelected = false;
  List<bool> _isSelectedList = [false, false, false];
  Gender _currentGender = Gender.notSelected;

  bool get isSelected => _isSelected;
  List<bool> get isSelectedList => _isSelectedList;
  Gender get currentGender => _currentGender;

  void changeCurrentGender(Gender value) {
    _currentGender = value;
    notifyListeners();
  }

  void setTrueToIsSelectedList(int index) {
    _isSelectedList = _isSelectedList.map((element) => false).toList();
    _isSelectedList[index] = true;
    _isSelected = true;
    notifyListeners();
  }
}
