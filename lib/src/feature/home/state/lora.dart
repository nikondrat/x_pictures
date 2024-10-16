import 'package:dio/dio.dart';
import 'package:flutter/foundation.dart';
import 'package:image_picker/image_picker.dart';
import 'package:mobx/mobx.dart';
import 'package:x_pictures/src/data.dart';

part 'lora.g.dart';

class LoraStore extends _LoraStore with _$LoraStore {
  LoraStore({required super.restClient});
}

abstract class _LoraStore with Store {
  final RestClient restClient;

  _LoraStore({required this.restClient});

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
    // TODO setted for debug and tests
    // if (!kDebugMode) {
    // router.pushNamed(AppViews.genderView, extra: {
    //   'store': store,
    //   'model': LoraModel(
    //       id: '',
    //       status: Status.completed,
    //       estimatedTime: 0,
    //       estimatedTimestamp: 0,
    //       trainingTimeSeconds: 0,
    //       images: [],
    //       cost: '',
    //       createdDate: DateTime.now()),
    // });

    if (kDebugMode) {
      router.pushNamed(AppViews.masterpieceView, extra: {
        'model': LoraModel(
            id: '',
            status: Status.completed,
            estimatedTime: 0,
            estimatedTimestamp: 0,
            trainingTimeSeconds: 0,
            images: [],
            cost: '',
            createdDate: DateTime.now()),
      });
    } else {
      // TODO use this for production
      FormData formData = FormData();

      for (int i = 0; i < photos.length; i++) {
        formData.files.add(
          MapEntry(
            'file${i + 1}',
            await MultipartFile.fromFile(
              photos[i].path,
              filename: photos[i].name,
            ),
          ),
        );
      }

      restClient
          .post(Endpoint().loras,
              body: formData, contentType: 'multipart/form-data')
          .then((v) {
        if (v?['detail'] == null) {
          final LoraModel model = LoraModel.fromJson(v!);
          router.pushNamed(AppViews.masterpieceView, extra: {
            'model': model,
          });
        }
      });
    }
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
