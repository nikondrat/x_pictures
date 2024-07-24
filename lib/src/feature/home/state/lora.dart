import 'dart:developer';
import 'dart:io';

import 'package:image_picker/image_picker.dart';
import 'package:mobx/mobx.dart';
import 'package:x_pictures/src/data.dart';

part 'lora.g.dart';

class LoraStore extends _LoraStore with _$LoraStore {
  LoraStore({required super.restClient, required super.store});
}

abstract class _LoraStore with Store {
  final RestClient restClient;
  final PacksStore store;

  _LoraStore({required this.restClient, required this.store});

  @observable
  ObservableList<XFile> photos = ObservableList();

  @computed
  int get photosLength => photos.length;

  @action
  void addPhotos(List<XFile> files) {
    photos.addAll(files);
  }

  @action
  void removePhoto(XFile file) {
    photos.remove(file);
  }

  @computed
  bool get canGenerateLora => photosLength <= 12;

  Future<void> generateLora() async {
    Map<String, List<int>> fileMap = {};

    for (int i = 0; i < photos.length; i++) {
      var file = photos[i];
      var filePath = file.path;

      if (File(filePath).existsSync()) {
        var fileContent = await File(filePath).readAsBytes();

        // Split the file content into lines and add it to the map
        // List<String> fileLines =
        //     fileContentString.split('\n').map((line) => line.trim()).toList();
        fileMap['file${i + 1}'] = fileContent;
      }
    }

    // Convert the map to the required format
    Map<String, Object?> body = Map<String, Object?>.from(fileMap);

    // Log the body
    // log('body: $body');

    // log('items: $photos');

    // log('body: $body');

    final future = restClient.post(Endpoint().loras, body: body).then((v) {
      log('$v');
    });

    router.pushNamed(AppViews.genderView, extra: {
      'store': store,
    });
  }
}
