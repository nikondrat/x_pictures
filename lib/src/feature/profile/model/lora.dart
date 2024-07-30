import 'package:json_annotation/json_annotation.dart';
import 'package:x_pictures/src/data.dart';

part 'lora.g.dart';

@JsonSerializable()
class LoraModel {
  @JsonKey()
  final String id;

  @JsonKey()
  final Status status;

  @JsonKey(name: 'estimated_time')
  final int estimatedTime;

  @JsonKey(name: 'estimated_timestamp')
  final int estimatedTimestamp;

  @JsonKey(name: 'training_time_seconds')
  final int? trainingTimeSeconds;

  @JsonKey(name: 'training_faces')
  final List<ImageModel> images;

  final String cost;

  @JsonKey(name: 'created')
  final DateTime createdDate;

  LoraModel({
    required this.id,
    required this.status,
    required this.estimatedTime,
    required this.estimatedTimestamp,
    required this.trainingTimeSeconds,
    required this.images,
    required this.cost,
    required this.createdDate,
  });

  factory LoraModel.fromJson(Map<String, dynamic> json) =>
      _$LoraModelFromJson(json);

  /// Connect the generated [_$LoraModelToJson] function to the `toJson` method.
  Map<String, dynamic> toJson() => _$LoraModelToJson(this);
}
