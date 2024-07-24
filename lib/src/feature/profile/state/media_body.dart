import 'package:mobx/mobx.dart';
import 'package:x_pictures/src/data.dart';

part 'media_body.g.dart';

class MediaBodyStore extends _MediaBodyStore with _$MediaBodyStore {
  MediaBodyStore();
}

abstract class _MediaBodyStore with Store {
  @observable
  ObservableList<MediaModel> items = ObservableList.of([
    MediaModel(
      type: MediaType.image,
      url:
          'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
      createdDate: DateTime(2024, 6, 10),
    ),
    MediaModel(
        type: MediaType.image,
        createdDate: DateTime(2024, 6, 10),
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.image,
        createdDate: DateTime(2024, 6, 10),
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.image,
        createdDate: DateTime(2024, 6, 10),
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.image,
        createdDate: DateTime(2024, 7, 8),
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.image,
        createdDate: DateTime(2024, 7, 6),
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.image,
        createdDate: DateTime(2024, 7, 4),
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.image,
        createdDate: DateTime(2024, 7, 6),
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.image,
        createdDate: DateTime(2024, 7, 6),
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.image,
        createdDate: DateTime(2024, 7, 6),
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.image,
        createdDate: DateTime(2024, 7, 3),
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.image,
        createdDate: DateTime(2024, 7, 3),
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.image,
        createdDate: DateTime(2024, 6, 10),
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.image,
        createdDate: DateTime(2024, 6, 10),
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.image,
        createdDate: DateTime(2024, 6, 10),
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.image,
        createdDate: DateTime(2024, 6, 10),
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
  ]);

  @computed
  Map<DateTime, List<MediaModel>> get groupedItems {
    Map<DateTime, List<MediaModel>> grouped = <DateTime, List<MediaModel>>{};
    for (var item in items) {
      if (grouped.containsKey(item.createdDate)) {
        grouped[item.createdDate]!.add(item);
      } else {
        grouped[item.createdDate] = [item];
      }
    }
    return grouped;
  }

  @computed
  ObservableList<MediaModel> get selectedItems =>
      ObservableList.of(items.where((item) => item.isSelected));

  @computed
  bool get isHasSelectedItems => selectedItems.isNotEmpty;

  @observable
  bool isSelect = false;

  @action
  void toggleSelect() {
    isSelect = !isSelect;

    if (!isSelect) {
      markAllNotSelected();
    }
  }

  @action
  void markAllNotSelected() {
    for (var item in items) {
      item.isSelected = false;
    }
    isSelect = false;
  }

  @action
  void markAllSelected() {
    for (var item in items) {
      item.isSelected = true;
    }
  }
}
