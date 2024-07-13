import 'package:mobx/mobx.dart';

part 'media.g.dart';

enum MediaType {
  image,
  video,
}

// class MediaModel {
//   final MediaType type;
//   final String url;

//   final DateTime createdDate;

//   MediaModel(
//       {required this.type, required this.url, required this.createdDate});
// }

class MediaModel extends _MediaModel with _$MediaModel {
  final MediaType type;
  final String url;

  final DateTime createdDate;
  MediaModel(
      {required this.type, required this.url, required this.createdDate});
}

abstract class _MediaModel with Store {
  @observable
  bool isSelected = false;

  @action
  void toggleSelected() {
    isSelected = !isSelected;
  }
}
