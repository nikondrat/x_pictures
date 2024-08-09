import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:flutter_mobx/flutter_mobx.dart';
import 'package:provider/provider.dart';
import 'package:x_pictures/src/core/constant/images.dart';
import 'package:x_pictures/src/core/constant/styles.dart';
import 'package:x_pictures/src/data.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:percent_indicator/percent_indicator.dart';

class MasterpieceView extends StatefulWidget {
  final PacksStore store;
  final LoraModel model;
  const MasterpieceView({super.key, required this.store, required this.model});

  @override
  State<MasterpieceView> createState() => _MasterpieceViewState();
}

class _MasterpieceViewState extends State<MasterpieceView> {
  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;

    return Provider(
      create: (context) => PhotosLoaderStore(
        store: widget.store,
        model: widget.model,
      ),
      builder: (context, child) {
        final store = Provider.of<PhotosLoaderStore>(context);
        return MasterpieceBody(store: store);
      },
    );
  }
}
