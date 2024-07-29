import 'package:flutter/material.dart';
import 'dart:async';
import 'package:x_pictures/src/data.dart';

class TimeIndicator extends ChangeNotifier {
  final int _totalTime = 5;
  int _start = 5;
  double _percent = 0;

  int get getCurrentTimeRemained => _start;
  double get currentPercent => _percent;

  void startTimer(PacksStore store) {
    const int oneSec = 1;

    Timer.periodic(const Duration(seconds: oneSec), (Timer timer) {
      if (_start == 0) {
        timer.cancel();
        router.goNamed(AppViews.photosView, extra: {
          "store": store,
          "models": [
            MediaModel(
                type: MediaType.image,
                url:
                    'https://mykaleidoscope.ru/x/uploads/posts/2023-12/1702643243_mykaleidoscope-ru-p-marlin-monro-pinterest-15.jpg',
                createdDate: DateTime.now()),
            MediaModel(
                type: MediaType.image,
                url:
                    'https://mykaleidoscope.ru/x/uploads/posts/2023-12/1702643243_mykaleidoscope-ru-p-marlin-monro-pinterest-15.jpg',
                createdDate: DateTime.now()),
            MediaModel(
                type: MediaType.image,
                url:
                    'https://mykaleidoscope.ru/x/uploads/posts/2023-12/1702643243_mykaleidoscope-ru-p-marlin-monro-pinterest-15.jpg',
                createdDate: DateTime.now()),
            MediaModel(
                type: MediaType.image,
                url:
                    'https://mykaleidoscope.ru/x/uploads/posts/2023-12/1702643243_mykaleidoscope-ru-p-marlin-monro-pinterest-15.jpg',
                createdDate: DateTime.now()),
            MediaModel(
                type: MediaType.image,
                url:
                    'https://mykaleidoscope.ru/x/uploads/posts/2023-12/1702643243_mykaleidoscope-ru-p-marlin-monro-pinterest-15.jpg',
                createdDate: DateTime.now()),
            MediaModel(
                type: MediaType.image,
                url:
                    'https://mykaleidoscope.ru/x/uploads/posts/2023-12/1702643243_mykaleidoscope-ru-p-marlin-monro-pinterest-15.jpg',
                createdDate: DateTime.now()),
            MediaModel(
                type: MediaType.image,
                url:
                    'https://mykaleidoscope.ru/x/uploads/posts/2023-12/1702643243_mykaleidoscope-ru-p-marlin-monro-pinterest-15.jpg',
                createdDate: DateTime.now()),
            MediaModel(
                type: MediaType.image,
                url:
                    'https://mykaleidoscope.ru/x/uploads/posts/2023-12/1702643243_mykaleidoscope-ru-p-marlin-monro-pinterest-15.jpg',
                createdDate: DateTime.now()),
            MediaModel(
                type: MediaType.image,
                url:
                    'https://mykaleidoscope.ru/x/uploads/posts/2023-12/1702643243_mykaleidoscope-ru-p-marlin-monro-pinterest-15.jpg',
                createdDate: DateTime.now()),
            MediaModel(
                type: MediaType.image,
                url:
                    'https://mykaleidoscope.ru/x/uploads/posts/2023-12/1702643243_mykaleidoscope-ru-p-marlin-monro-pinterest-15.jpg',
                createdDate: DateTime.now()),
          ]
          // 'model': model,
          // 'urls': [
          //   'https://mykaleidoscope.ru/x/uploads/posts/2023-12/1702643243_mykaleidoscope-ru-p-marlin-monro-pinterest-15.jpg',
          //   'https://mykaleidoscope.ru/x/uploads/posts/2023-12/1702643243_mykaleidoscope-ru-p-marlin-monro-pinterest-15.jpg',
          //   'https://mykaleidoscope.ru/x/uploads/posts/2023-12/1702643243_mykaleidoscope-ru-p-marlin-monro-pinterest-15.jpg',
          //   'https://mykaleidoscope.ru/x/uploads/posts/2023-12/1702643243_mykaleidoscope-ru-p-marlin-monro-pinterest-15.jpg',
          //   'https://mykaleidoscope.ru/x/uploads/posts/2023-12/1702643243_mykaleidoscope-ru-p-marlin-monro-pinterest-15.jpg',
          //   'https://mykaleidoscope.ru/x/uploads/posts/2023-12/1702643243_mykaleidoscope-ru-p-marlin-monro-pinterest-15.jpg',
          //   'https://mykaleidoscope.ru/x/uploads/posts/2023-12/1702643243_mykaleidoscope-ru-p-marlin-monro-pinterest-15.jpg',
          //   'https://mykaleidoscope.ru/x/uploads/posts/2023-12/1702643243_mykaleidoscope-ru-p-marlin-monro-pinterest-15.jpg',
          //   'https://mykaleidoscope.ru/x/uploads/posts/2023-12/1702643243_mykaleidoscope-ru-p-marlin-monro-pinterest-15.jpg',
          //   'https://mykaleidoscope.ru/x/uploads/posts/2023-12/1702643243_mykaleidoscope-ru-p-marlin-monro-pinterest-15.jpg',
          // ]
        });
      } else {
        _start--;
        _percent = 1 - (_start / _totalTime);
        notifyListeners();
      }
    });
  }
}
