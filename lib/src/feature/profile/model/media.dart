import 'package:json_annotation/json_annotation.dart';
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

@JsonSerializable()
class MediaModel extends _MediaModel with _$MediaModel {
  @JsonKey()
  final int? id;

  final MediaType? type;

  @JsonKey(name: 'image')
  final String url;

  @JsonKey()
  final int? sort;

  @JsonKey(name: 'created')
  final DateTime? createdDate;

  MediaModel({
    this.type,
    required this.url,
    this.createdDate,
    this.id,
    this.sort,
  });

  factory MediaModel.fromJson(Map<String, dynamic> json) =>
      _$MediaModelFromJson(json);

  /// Connect the generated [_$MediaModelToJson] function to the `toJson` method.
  Map<String, dynamic> toJson() => _$MediaModelToJson(this);
}

abstract class _MediaModel with Store {
  @observable
  @JsonKey(
    includeFromJson: false,
    includeToJson: false,
  )
  bool isSelected = false;

  @action
  void toggleSelected() {
    isSelected = !isSelected;
  }
}
