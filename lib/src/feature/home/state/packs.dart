import 'package:mobx/mobx.dart';
import 'package:x_pictures/src/data.dart';

part 'packs.g.dart';

class PacksStore extends _PacksStore with _$PacksStore {
  PacksStore({required super.restClient});
}

abstract class _PacksStore with Store {
  final RestClient restClient;

  _PacksStore({required this.restClient});

  PackBody body =
      PackBody(count: 0, total: 0, nextUrl: '', previousUrl: '', packs: []);

  @observable
  ObservableFuture<List<PackModel>> fetchPacksFuture = emptyResponse;

  @action
  Future<List<PackModel>> fetchPacks() async {
    final future = restClient.get(Endpoint().packs).then((v) {
      body = PackBody.fromJson(v!);

      return body.packs;
    });
    fetchPacksFuture = ObservableFuture(future);
    return await future;
  }

  @computed
  bool get hasResults =>
      fetchPacksFuture != emptyResponse &&
      fetchPacksFuture.status == FutureStatus.fulfilled;

  static ObservableFuture<List<PackModel>> emptyResponse =
      ObservableFuture.value([]);
}
