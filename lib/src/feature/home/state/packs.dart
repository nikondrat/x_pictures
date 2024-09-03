import 'dart:developer';

import 'package:collection/collection.dart';
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

  @observable
  ObservableList<PackModel> packs = ObservableList();

  @observable
  PackModel selected =
      PackModel(id: 0, title: '', description: '', category: '', images: []);

  @action
  Future setSelectedPack(PackModel value) async {
    selected = value;
  }

  @computed
  Map<String, List<PackModel>> get groupedPacks =>
      groupBy(packs, (PackModel pack) => pack.category);

  @observable
  int page = 1;

  @action
  void selectPage(int value) => page = value;

  @action
  Future nextPage() async {
    if (body.nextUrl != null) {
      page++;
      fetchPacks();
    }
  }

  @action
  Future<List<PackModel>> fetchPacks() async {
    final future = restClient.get(Endpoint().packs, queryParams: {
      'page': '$page',
    }).then((v) {
      body = PackBody.fromJson(v!);

      return body.packs;
    });

    fetchPacksFuture = ObservableFuture(future);
    if (page == 1) {
      return packs = ObservableList.of(await future);
    } else {
      packs.addAll(await future);
    }

    return packs;
  }

  @computed
  bool get hasResults =>
      fetchPacksFuture != emptyResponse &&
      fetchPacksFuture.status == FutureStatus.fulfilled;

  static ObservableFuture<List<PackModel>> emptyResponse =
      ObservableFuture.value([]);
}
