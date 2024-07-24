import 'package:mobx/mobx.dart';
import 'package:x_pictures/src/data.dart';

part 'media.g.dart';

class MediaStore extends _MediaStore with _$MediaStore {
  MediaStore({required super.restClient});
}

abstract class _MediaStore with Store {
  final RestClient restClient;

  _MediaStore({required this.restClient});

  LorasBody body = LorasBody(
    count: 0,
    total: 0,
    nextUrl: '',
    previousUrl: '',
    loras: [],
  );

  @observable
  ObservableFuture<List<LoraModel>> fetchLorasFuture = emptyResponse;

  @action
  Future<List<LoraModel>> fetchLoras() async {
    final future = restClient.get(Endpoint().loras).then((v) {
      body = LorasBody.fromJson(v!);

      return body.loras;
    }).catchError((v) {
      // TODO only for dev
      return LorasBody(
        count: 0,
        total: 0,
        nextUrl: '',
        previousUrl: '',
        loras: [
          LoraModel(
            id: '',
            status: Status.completed,
            createdDate: DateTime.now(),
            estimatedTime: '',
            estimatedTimestamp: '',
            trainingTimeSeconds: 0,
            images: [],
            cost: '',
          )
        ],
      ).loras;
    });
    fetchLorasFuture = ObservableFuture(future);
    return await future;
  }

  @computed
  bool get hasResults =>
      fetchLorasFuture != emptyResponse &&
      fetchLorasFuture.status == FutureStatus.fulfilled;

  static ObservableFuture<List<LoraModel>> emptyResponse =
      ObservableFuture.value([]);
}
