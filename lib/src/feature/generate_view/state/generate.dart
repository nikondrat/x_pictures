import 'package:mobx/mobx.dart';
import 'package:x_pictures/src/data.dart';

part 'generate.g.dart';

class GenerateStore extends _GenerateStore with _$GenerateStore {
  GenerateStore({required super.restClient, required super.viewStore});
}

abstract class _GenerateStore with Store {
  final RestClient restClient;
  final GenerateViewStore viewStore;

  _GenerateStore({required this.restClient, required this.viewStore});

  @observable
  ObservableFuture<GenerateFilter> data = emptyResponse;

  @computed
  ObservableList<Tag> get tags => ObservableList.of(data.value?.tags ?? []);

  @computed
  ObservableList<SdModel> get sdModels =>
      ObservableList.of(data.value?.sdModels ?? []);

  @computed
  ObservableList<ActionModel> get actions =>
      ObservableList.of(data.value?.actions ?? []);

  @action
  Future<GenerateFilter> fetchFilter() async {
    final future = restClient.get(Endpoint().filtersForGenerate).then((v) {
      final body = GenerateFilter.fromJson(v!);

      viewStore.setSelectedStyle(body.currentSDModel ?? 0);

      return body;
    });
    return data = ObservableFuture(future);
  }

  void generate() {
    restClient.post(Endpoint().whiteGenerate, body: {
      "sd_model_id": viewStore.selectedStyle,
      "prompt": viewStore.controller.text,
      // "negative_prompt": "low resolution, low details",
    }).then((v) {
      final GenerateResponse body = GenerateResponse.fromJson(v!);

      router.goNamed(AppViews.resultView, extra: {'response': body});
    });
  }

  @computed
  bool get hasResults =>
      data != emptyResponse && data.status == FutureStatus.fulfilled;

  static ObservableFuture<GenerateFilter> emptyResponse =
      ObservableFuture.value(GenerateFilter(
    cost: 0,
    currentSDModel: 0,
    tags: [],
    sdModels: [],
    actions: [],
  ));
}
