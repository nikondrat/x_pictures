// class PackModel {
//   final String title;
//   final int length;
//   final int? progress;
//   final List<String> urls;
//   PackModel({
//     required this.title,
//     required this.length,
//     this.progress,
//     required this.urls,
//   });
// }

import 'package:json_annotation/json_annotation.dart';
import 'package:mobx/mobx.dart';
import 'package:x_pictures/src/data.dart';

part 'pack.g.dart';

@JsonSerializable()
class PackModel extends _PackModel with _$PackModel {
  @JsonKey()
  final int id;

  @JsonKey(name: 'name')
  final String title;

  @JsonKey()
  final String description;

  @JsonKey()
  final String category;

  PackModel({
    required this.id,
    required this.title,
    required this.description,
    required this.category,
    required super.images,
  });

  factory PackModel.fromJson(Map<String, dynamic> json) =>
      _$PackModelFromJson(json);

  /// Connect the generated [_$PackModelToJson] function to the `toJson` method.
  Map<String, dynamic> toJson() => _$PackModelToJson(this);
}

abstract class _PackModel with Store {
  _PackModel({required this.images});

  @JsonKey()
  @observable
  List<ImageModel> images;

  @computed
  int get length => images.length;
}
