import 'package:json_annotation/json_annotation.dart';

part 'sd_model.g.dart';

@JsonSerializable()
class SdModel {
  @JsonKey()
  final int id;

  @JsonKey()
  final String title;

  @JsonKey(name: 'image')
  final String? imageUrl;

  @JsonKey(name: 'is_lock')
  final bool isLock;

  @JsonKey(name: 'available_in')
  final int? availableIn;

  SdModel({
    required this.id,
    required this.title,
    required this.imageUrl,
    required this.isLock,
    required this.availableIn,
  });

  factory SdModel.fromJson(Map<String, dynamic> json) =>
      _$SdModelFromJson(json);

  /// Connect the generated [_$SdModelToJson] function to the `toJson` method.
  Map<String, dynamic> toJson() => _$SdModelToJson(this);
}
