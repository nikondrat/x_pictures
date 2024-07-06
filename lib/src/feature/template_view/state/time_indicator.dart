import 'package:flutter/material.dart';
import 'dart:async';

class TimeIndicator extends ChangeNotifier {
  final int _totalTime = 5;
  int _start = 5;
  double _percent = 0;

  int get getCurrentTimeRemained => _start;
  double get currentPercent => _percent;


  void startTimer() {
    const int oneSec = 1;
    Timer.periodic(const Duration(seconds: oneSec),
        (Timer timer) {
          if (_start == 0)
            {
              timer.cancel();
            } else {
            _start--;
            _percent = 1 - (_start / _totalTime);
            notifyListeners();
          }
        }
    );
  }
}