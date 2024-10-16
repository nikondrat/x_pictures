import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:x_pictures/src/data.dart';

class DocumentView extends StatelessWidget {
  final String title;
  final String filePath;
  const DocumentView({super.key, required this.title, required this.filePath});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;

    return Scaffold(
      appBar: AppBar(
        leading: const CustomBackButton(),
        title: Text(
          title,
          style: textTheme.bodyMedium!.copyWith(
            fontWeight: FontWeight.w700,
            fontSize: 17,
          ),
        ),
      ),
      body: AppBody(
        builder: (windowWidth, __, ___) => Padding(
          padding: HorizontalSpacing.centered(windowWidth),
          // child: Text('dgdfgd'),
          child: FutureBuilder<String>(
              future: DefaultAssetBundle.of(context).loadString(filePath),
              builder: (context, snapshot) {
                if (snapshot.connectionState == ConnectionState.done &&
                    snapshot.hasData) {
                  return AutoSizeText(
                    snapshot.data ?? '',
                    style: textTheme.bodyLarge!
                        .copyWith(color: AppColors.kOutlineColor),
                  );
                }

                return const SizedBox.shrink();
              }),
        ),
      ),
    );
  }
}
