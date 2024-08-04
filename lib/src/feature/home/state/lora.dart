import 'package:dio/dio.dart';
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

    final future = restClient
        .post(Endpoint().loras,
            body: formData, contentType: 'multipart/form-data')
        .then((v) {
      if (v?['detail'] == null) {
        final LoraModel model = LoraModel.fromJson(v!);
        router.pushNamed(AppViews.genderView, extra: {
          'store': store,
          'model': model,
        });
      }
    });

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
