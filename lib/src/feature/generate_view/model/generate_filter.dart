import 'package:json_annotation/json_annotation.dart';
import 'package:x_pictures/src/data.dart';

part 'generate_filter.g.dart';

@JsonSerializable()
class GenerateFilter {
  @JsonKey()
  final double? cost;

  @JsonKey(name: 'current_sd_model_id')
  final int? currentSDModel;

  @JsonKey()
  final List<Tag>? tags;

  @JsonKey(name: 'sd_models')
  final List<SdModel>? sdModels;

  @JsonKey()
  final List<ActionModel>? actions;

  GenerateFilter({
    required this.cost,
    required this.currentSDModel,
    required this.tags,
    required this.sdModels,
    required this.actions,
  });

  factory GenerateFilter.fromJson(Map<String, dynamic> json) =>
      _$GenerateFilterFromJson(json);

  /// Connect the generated [_$GenerateFilterToJson] function to the `toJson` method.
  Map<String, dynamic> toJson() => _$GenerateFilterToJson(this);
}
