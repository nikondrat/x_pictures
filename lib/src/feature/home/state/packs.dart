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

  @observable
  int carouselIndex = 0;

  @action
  void setCarouselIndex(int value) {
    carouselIndex = value;
  }

  PackBody body =
      PackBody(count: 0, total: 0, nextUrl: '', previousUrl: '', packs: []);

  @observable
  ObservableFuture<List<PackModel>> fetchPacksFuture = emptyResponse;

  @observable
  ObservableList<PackModel> packs = ObservableList();

  @computed
  PackModel get pack => body.packs.isNotEmpty
      ? body.packs.first
      : PackModel(id: 0, title: '', description: '', category: '', images: [
          MediaModel(
              url:
                  'https://x-pictures-back-main.s3.us-east-2.amazonaws.com/media/face2img_packs_default_images/58ac1659-7a6d-4e9e-908e-5c0f7cb9fadd.png')
        ]);

  @observable
  PackModel selected =
      PackModel(id: 0, title: '', description: '', category: '', images: []);

  @action
  Future setSelectedPack(PackModel value) async {
    selected = value;
  }

  @observable
  String query = '';

  @action
  void setQuery(String value) {
    query = value;
  }

  @computed
  Map<String, List<PackModel>> get groupedPacks {
    if (query.isEmpty) {
      return groupBy(packs, (PackModel pack) => pack.category);
    } else {
      final List<PackModel> filtered = packs
          .where((pack) =>
              pack.category.toLowerCase().contains(query.toLowerCase()) ||
              pack.title.toLowerCase().contains(query.toLowerCase()))
          .toList();

      return groupBy(filtered, (PackModel pack) => pack.category);
    }
  }

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
