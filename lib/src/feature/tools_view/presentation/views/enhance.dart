import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:gap/gap.dart';
import 'package:provider/provider.dart';
import 'package:x_pictures/src/data.dart';

class EnhanceView extends StatelessWidget {
  const EnhanceView({super.key});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;

    final PacksStore store = context.watch();

    return StudyingView(
      url:
          'https://get.wallhere.com/photo/face-women-model-portrait-long-hair-photography-Person-skin-Violetta-child-girl-beauty-smile-eye-woman-portrait-photography-photo-shoot-brown-hair-facial-expression-close-up-121398.jpg',
      child: AppBody(builder: (windowWidth, windowHeight, windowSize) {
        return Scaffold(
          appBar: AppBar(
            leading: const CustomBackButton(),
            actions: [
              Padding(
                padding: const EdgeInsets.all(8.0),
                child: IconButton(
                  onPressed: () {},
                  icon: const Icon(Icons.file_download_outlined),
                ),
              )
            ],
          ),
          body: EnhanceBody(
            model: store.selected,
          ),
          // body: Center(
          //   child: ClipRRect(
          //       borderRadius: BorderRadius.circular(AppValues.kRadius),
          //       child: CachedNetworkImage(imageUrl: model.url)),
          // ),
          bottomNavigationBar: Padding(
            padding: HorizontalSpacing.centered(windowWidth),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                SizedBox(
                  height: 200,
                  child: Row(
                    children: [
                      'https://image.winudf.com/v2/image1/Y29tLnJlYWltYWdpbmUuZW5oYW5jZWl0X3NjcmVlbl9ydS1SVV8wXzE2NjY1ODQyNDNfMDE3/screen-0.jpg?fakeurl=1&type=.jpg',
                      'https://image.winudf.com/v2/image1/Y29tLnJlYWltYWdpbmUuZW5oYW5jZWl0X3NjcmVlbl9ydS1SVV8wXzE2NjY1ODQyNDNfMDE3/screen-0.jpg?fakeurl=1&type=.jpg',
                      'https://image.winudf.com/v2/image1/Y29tLnJlYWltYWdpbmUuZW5oYW5jZWl0X3NjcmVlbl9ydS1SVV8wXzE2NjY1ODQyNDNfMDE3/screen-0.jpg?fakeurl=1&type=.jpg',
                      'https://image.winudf.com/v2/image1/Y29tLnJlYWltYWdpbmUuZW5oYW5jZWl0X3NjcmVlbl9ydS1SVV8wXzE2NjY1ODQyNDNfMDE3/screen-0.jpg?fakeurl=1&type=.jpg',
                    ]
                        .map((e) => Expanded(
                              child: Padding(
                                padding: const EdgeInsets.all(
                                    AppValues.kPadding / 2),
                                child: ClipRRect(
                                    borderRadius: BorderRadius.circular(
                                        AppValues.kRadius),
                                    child: Stack(
                                      fit: StackFit.expand,
                                      children: [
                                        ImageWithShader(url: e),
                                        Align(
                                            alignment: Alignment.bottomCenter,
                                            child: Padding(
                                              padding: const EdgeInsets.only(
                                                  bottom:
                                                      AppValues.kPadding / 2),
                                              child: AutoSizeText(
                                                  store.selected.title),
                                            ))
                                      ],
                                    )),
                              ),
                            ))
                        .toList(),
                  ),
                ),
                Gap(AppValues.kPadding),
                Text(
                  t.homeView.styles.smart_tool.types.enhance,
                  textAlign: TextAlign.center,
                  style: textTheme.bodyLarge,
                ),
                Gap(AppValues.kPadding),
              ],
            ),
          ),
        );
      }),
    );
  }
}
