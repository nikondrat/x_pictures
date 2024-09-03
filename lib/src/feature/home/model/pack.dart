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

  @JsonKey()
  final Subcategory? subcategory;

  PackModel({
    required this.id,
    required this.title,
    required this.description,
    required this.category,
    required super.images,
    this.subcategory,
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
  List<MediaModel> images;

  @computed
  int get length => images.length;
}

enum Subcategory {
  @JsonValue('Athlete')
  athlete,

  @JsonValue('Avatar')
  avatar,

  @JsonValue('Beach')
  beach,

  @JsonValue('Black & white')
  blackAndWhite,

  @JsonValue('Black background')
  blackBackground,

  @JsonValue('Blond')
  blond,

  @JsonValue('Bob cut')
  bobCut,

  @JsonValue('Bora bora')
  boraBora,

  @JsonValue('Breaking bad')
  breakingBad,

  @JsonValue('Brown hair')
  brownHair,

  @JsonValue('Burberry')
  burberry,

  @JsonValue('Business')
  business,

  @JsonValue('Buzz cut')
  buzzCut,

  @JsonValue('Cappadocia')
  cappadocia,

  @JsonValue('Casual')
  casual,

  @JsonValue('Casual selfie')
  casualSelfie,

  @JsonValue('Chanel')
  chanel,

  @JsonValue('Chloe')
  chloe,

  @JsonValue('Clinique yerde')
  cliniqueYerde,

  @JsonValue('Coffee date')
  coffeeDate,

  @JsonValue('Colesseum')
  colesseum,

  @JsonValue('Colorful hair')
  colorfulHair,

  @JsonValue('Curly')
  curly,

  @JsonValue('Date')
  date,

  @JsonValue('Desperate housewives')
  desperateHousewives,

  @JsonValue('Dior')
  dior,

  @JsonValue('Dubai')
  dubai,

  @JsonValue('Eiffel Tower')
  eiffelTower,

  @JsonValue('Elite')
  elite,

  @JsonValue('Enhance')
  enhance,

  @JsonValue('Friends')
  friends,

  @JsonValue('Game of Thrones')
  gameOfThrones,

  @JsonValue('Ginger')
  ginger,

  @JsonValue('Golf')
  golf,

  @JsonValue('Goth')
  goth,

  @JsonValue('Grand Canyon')
  grandCanyon,

  @JsonValue('Hermes')
  hermes,

  @JsonValue('Hip hop')
  hipHop,

  @JsonValue('Hong Kong')
  hongKong,

  @JsonValue('Horse riding')
  horseRiding,

  @JsonValue('Istanbul')
  istanbul,

  @JsonValue('Japan')
  japan,

  @JsonValue('Look book')
  lookBook,

  @JsonValue('Louis Vuitton')
  louisVuitton,

  @JsonValue('Luxury')
  luxury,

  @JsonValue('Maldives')
  maldives,

  @JsonValue('Marvel')
  marvel,

  @JsonValue('Milan')
  milan,

  @JsonValue('Monaco')
  monaco,

  @JsonValue('Monochrome Polaroid')
  monochromePolaroid,

  @JsonValue('Munich')
  munich,

  @JsonValue('Nerd')
  nerd,

  @JsonValue('Niagara Falls')
  niagaraFalls,

  @JsonValue('Office')
  office,

  @JsonValue('Old money')
  oldMoney,

  @JsonValue('Opera')
  opera,

  @JsonValue('Podium')
  podium,

  @JsonValue('Polaroid')
  polaroid,

  @JsonValue('Prada')
  prada,

  @JsonValue('Private jet')
  privateJet,

  @JsonValue('Prom skater')
  promSkater,

  @JsonValue('Red carpet')
  redCarpet,

  @JsonValue('Remove BG')
  removeBg,

  @JsonValue('Remove objects')
  removeObjects,

  @JsonValue('Santorini')
  santorini,

  @JsonValue('Street style')
  streetStyle,

  @JsonValue('Studio shooting')
  studioShooting,

  @JsonValue('Suicide Squad')
  suicideSquad,

  @JsonValue('Suit')
  suit,

  @JsonValue('Switzerland')
  switzerland,

  @JsonValue('Sydney')
  sydney,

  @JsonValue('Tak mahal')
  takMahal,

  @JsonValue('Tennis')
  tennis,

  @JsonValue('The 1940s')
  the1940s,

  @JsonValue('The 1950s')
  the1950s,

  @JsonValue('The 1960s')
  the1960s,

  @JsonValue('The 1970s')
  the1970s,

  @JsonValue('The 1980s')
  the1980s,

  @JsonValue('The 1980s arcade')
  the1980sArcade,

  @JsonValue('The 1990s')
  the1990s,

  @JsonValue('The 2000s')
  the2000s,

  @JsonValue('The hunger games')
  theHungerGames,

  @JsonValue('The last of us')
  theLastOfUs,

  @JsonValue('The walking dead')
  theWalkingDead,

  @JsonValue('Venice')
  venice,

  @JsonValue('Wedding')
  wedding,

  @JsonValue('White background')
  whiteBackground,

  @JsonValue('Yacht')
  yacht,

  @JsonValue('Yves Saint Laurent')
  yvesSaintLaurent,
}
