import 'package:json_annotation/json_annotation.dart';

import 'package:x_pictures/src/data.dart';

part 'loras_body.g.dart';

@JsonSerializable()
class LorasBody extends PageModel {
  LorasBody(
      {required super.count,
      required super.total,
      required super.nextUrl,
      required super.previousUrl,
      required this.loras});

  @JsonKey(name: 'results')
  final List<LoraModel> loras;

  factory LorasBody.fromJson(Map<String, dynamic> json) =>
      _$LorasBodyFromJson(json);

  /// Connect the generated [_$LorasBodyToJson] function to the `toJson` method.
  @override
  Map<String, dynamic> toJson() => _$LorasBodyToJson(this);
}
