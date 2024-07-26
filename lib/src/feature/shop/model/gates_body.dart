import 'package:json_annotation/json_annotation.dart';
import 'package:x_pictures/src/data.dart';

part 'gates_body.g.dart';

@JsonSerializable()
class GatesBody extends PageModel {
  @JsonKey(name: 'results')
  final List<Gate> gates;

  GatesBody({
    required super.count,
    required super.total,
    required super.nextUrl,
    required super.previousUrl,
    required this.gates,
  });

  factory GatesBody.fromJson(Map<String, dynamic> json) =>
      _$GatesBodyFromJson(json);

  /// Connect the generated [_$GatesBodyToJson] function to the `toJson` method.
  Map<String, dynamic> toJson() => _$GatesBodyToJson(this);
}
