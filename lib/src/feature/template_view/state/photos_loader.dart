import 'dart:async';

import 'package:flutter/foundation.dart';
import 'package:mobx/mobx.dart';
import 'package:x_pictures/src/data.dart';

part 'photos_loader.g.dart';

class PhotosLoaderStore extends _PhotosLoaderStore with _$PhotosLoaderStore {
  PhotosLoaderStore({required super.store, required super.model});
}

abstract class _PhotosLoaderStore with Store {
  final PacksStore store;
  final LoraModel model;

  _PhotosLoaderStore({required this.store, required this.model});

  Timer? _timer;

  @observable
  int seconds = 5;

  @computed
  double get percent => seconds / 5;

  @action
  void startTimer() {
    _timer = Timer.periodic(const Duration(seconds: 1), (timer) {
      if (seconds == 0) {
        return stopTimer();
      }
      seconds--;
    });
  }

  @action
  void stopTimer() {
    dispose();
    router.goNamed(AppViews.photosView, extra: {
      "model": model,
      "store": store,
      "models": !kDebugMode
          ? model.images
          : [
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
    });
  }

  @action
  void resetTimer() {
    _timer?.cancel();
    seconds = 0;
  }

  @action
  void dispose() {
    _timer?.cancel();
    _timer = null;
  }
}
