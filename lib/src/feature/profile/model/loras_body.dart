import 'package:json_annotation/json_annotation.dart';

import 'package:mobx/mobx.dart';
import 'package:x_pictures/src/data.dart';

part 'loras_body.g.dart';

@JsonSerializable()
class LorasBody extends _LorasBody with _$LorasBody {
  @JsonKey()
  final int count;

  @JsonKey(name: 'num_pages')
  final int total;

  @JsonKey(name: 'next')
  final String? nextUrl;

  @JsonKey(name: 'previous')
  final String? previousUrl;

  @JsonKey(name: 'results')
  final List<LoraModel> loras;

  LorasBody({
    required this.count,
    required this.total,
    required this.nextUrl,
    required this.previousUrl,
    required this.loras,
  });

  factory LorasBody.fromJson(Map<String, dynamic> json) =>
      _$LorasBodyFromJson(json);

  /// Connect the generated [_$LorasBodyToJson] function to the `toJson` method.
  Map<String, dynamic> toJson() => _$LorasBodyToJson(this);
}

abstract class _LorasBody with Store {
  _LorasBody();

  @observable
  @JsonKey(includeToJson: false, includeFromJson: false)
  int selectedPage = 0;

  @action
  void selectPage(int index) {
    selectedPage = index;
  }
}
