import 'dart:async';

import 'package:mobx/mobx.dart';
import 'package:x_pictures/src/data.dart';

part 'photos_loader.g.dart';

class PhotosLoaderStore extends _PhotosLoaderStore with _$PhotosLoaderStore {
  PhotosLoaderStore({required super.model});
}

abstract class _PhotosLoaderStore with Store {
  final LoraModel model;

  _PhotosLoaderStore({required this.model});

  // Timer? _timer;

  // late int seconds = model.trainingTimeSeconds ?? 0;

  // @computed
  // double get percent => seconds / 5;

  // @action
  // void startTimer() {
  //   _timer = Timer.periodic(const Duration(minutes: 1), (timer) {
  //     if (seconds == 0) {
  //       return stopTimer();
  //     }
  //     print(seconds);
  //     seconds--;
  //   });
  // }

  @action
  void stopTimer() {
    router.goNamed(AppViews.photosView, extra: {
      "model": model,
      "models": model.images.isNotEmpty
          ? model.images
          :
          // !kDebugMode
          //     ? model.images
          //     :
          [
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

  // @action
  // void resetTimer() {
  //   _timer?.cancel();
  //   seconds = 0;
  // }

  // @action
  // void dispose() {
  //   _timer?.cancel();
  //   _timer = null;
  // }
}
