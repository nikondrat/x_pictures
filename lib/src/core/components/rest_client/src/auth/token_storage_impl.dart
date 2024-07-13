import 'dart:async';

import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:x_pictures/src/data.dart';

class TokenStorageImpl implements TokenStorage<Future<String?>> {
  final FlutterSecureStorage storage;

  TokenStorageImpl({required this.storage});

  static const _accessTokenKey = 'access';
  // static const _refreshTokenKey = 'refresh';

  @override
  Future<void> clearTokenPair() async {
    storage.delete(key: _accessTokenKey);
    // storage.delete(key: _refreshTokenKey);
  }

  @override
  Future<void> close() {
    // TODO: implement close
    throw UnimplementedError();
  }

  @override
  Stream<Future<String?>> getTokenPairStream() {
    final controller = StreamController<Future<String?>>();
    storage.read(key: _accessTokenKey).then((value) async {
      controller.add(Future.value(value));
      controller.close();
    }).catchError((error) {
      controller.addError(error);
      controller.close();
    });
    return controller.stream;
  }

  @override
  Future<Future<String?>> loadTokenPair() async {
    final Future<String?> accessToken = storage.read(key: _accessTokenKey);
    return Future.value(accessToken);
  }

  @override
  Future<void> saveTokenPair(accessToken) async {
    storage.write(key: _accessTokenKey, value: await accessToken);
  }
}
