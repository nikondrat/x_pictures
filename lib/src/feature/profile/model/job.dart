import 'package:json_annotation/json_annotation.dart';
import 'package:x_pictures/src/data.dart';

part 'job.g.dart';

@JsonSerializable()
class JobModel {
  @JsonKey(name: 'id')
  final int id;

  @JsonKey(name: 'lora')
  final LoraModel lora;

  @JsonKey()
  final PackModel pack;

  @JsonKey(name: 'results')
  final List<ImageModel> images;

  @JsonKey(name: 'time_spent')
  final int timeSpent;

  @JsonKey(name: 'estimated_time')
  final int estimatedTime;

  @JsonKey(name: 'estimated_timestamp')
  final int estimatedTimestamp;

  @JsonKey(name: 'status')
  final Status status;

  @JsonKey(name: 'cost')
  final String cost;

  @JsonKey(name: 'created')
  final DateTime createdDate;

  JobModel(
      {required this.id,
      required this.lora,
      required this.pack,
      required this.images,
      required this.timeSpent,
      required this.estimatedTime,
      required this.estimatedTimestamp,
      required this.status,
      required this.cost,
      required this.createdDate});

  factory JobModel.fromJson(Map<String, dynamic> json) =>
      _$JobModelFromJson(json);

  /// Connect the generated [_$JobModelToJson] function to the `toJson` method.
  Map<String, dynamic> toJson() => _$JobModelToJson(this);
}
