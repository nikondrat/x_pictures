import 'dart:developer';
import 'dart:io';

import 'package:dio/dio.dart';
import 'package:image_picker/image_picker.dart';
import 'package:mobx/mobx.dart';
import 'package:path/path.dart' as p;
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
    // FormData formData = FormData();

    // for (int i = 0; i < photos.length; i++) {
    //   formData.files.add(
    //     MapEntry(
    //       'file${i + 1}', // Имя поля, под которым сервер ожидает файл
    //       await MultipartFile.fromFile(
    //         photos[i].path,
    //         filename: photos[i].name,
    //       ),
    //     ),
    //   );
    // }

    // Map<String, MultipartFile> fileMap = {};

    // for (var i = 0; i < photos.length; i++) {
    //   File file = File(photos[i].path);
    //   String fileName = p.basename(file.path);
    //   fileMap['file$i'] = MultipartFile(file.openRead(), await file.length(),
    //       filename: fileName);
    // }

    // var data = FormData.fromMap(fileMap);

    // final future = restClient
    //     .post(Endpoint().loras, body: data, contentType: 'multipart/form-data')
    //     .then((v) {
    //   log('$v');
    // });

    router.pushNamed(AppViews.genderView, extra: {
      'store': store,
    });
  }

  @observable
  ObservableFuture<List<LoraModel>> fetchLorasFuture = emptyResponse;

  @observable
  ObservableList<LoraModel> loras = ObservableList();

  @action
  Future<List<LoraModel>> fetchLoras() async {
    final future = restClient.get(Endpoint().loras).then((v) {
      final LorasBody body = LorasBody.fromJson(v!);
      return body.loras;
    });

    fetchLorasFuture = ObservableFuture(future);
    return loras = ObservableList.of(await future);
  }

  Future<LoraModel?> getLora(String id) async {
    final future = restClient.get('${Endpoint().loras}/$id').then((v) {
      final LoraModel loraModel = LoraModel.fromJson(v!);
      return loraModel;
    });
    return await future;
  }

  @computed
  bool get hasResults => fetchLorasFuture.status == FutureStatus.fulfilled;

  static ObservableFuture<List<LoraModel>> emptyResponse =
      ObservableFuture.value([]);
}
