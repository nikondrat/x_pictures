enum MediaType {
  image,
  video,
}

class MediaModel {
  final MediaType type;
  final String url;

  MediaModel({required this.type, required this.url});
}
