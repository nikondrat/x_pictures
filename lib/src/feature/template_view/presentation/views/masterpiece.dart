import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:x_pictures/src/core/constant/images.dart';
import 'package:x_pictures/src/core/constant/styles.dart';
import 'package:x_pictures/src/data.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:percent_indicator/percent_indicator.dart';

class MasterpieceView extends StatefulWidget {
  final StyleModel model;
  const MasterpieceView({super.key, required this.model});

  @override
  State<MasterpieceView> createState() => _MasterpieceViewState();
}

class _MasterpieceViewState extends State<MasterpieceView> {
  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (context) => TimeIndicator(),
      child: Scaffold(
        /*appBar: AppBar(
          leading: const CustomBackButton(),
        ),*/
        body: Padding(
          padding: const EdgeInsets.all(AppValues.kPadding),
          child: Container(
            decoration: BoxDecoration(
                image: const DecorationImage(
                    image: AssetImage(
                      AppImages.bannerNoSign,
                    ),
                    fit: BoxFit.cover),
                borderRadius: BorderRadius.circular(AppValues.kRadius)),
            child: SizedBox(
              width: MediaQuery.of(context).size.width,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.center,
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  Text(
                    'We are creating a masterpiece...',
                    style: AppStyles.head1TextStyle,
                    textAlign: TextAlign.center,
                  ),
                  SizedBox(
                    height: 10.h,
                  ),
                  Consumer<TimeIndicator>(
                      builder: (context, consumerValue, child) {
                    consumerValue.startTimer();
                    if (consumerValue.getCurrentTimeRemained == 0) {}
                    return CircularPercentIndicator(
                      radius: 100.w,
                      animation: true,
                      animationDuration: 800,
                      animateFromLastPercent: true,
                      percent: consumerValue.currentPercent,
                      lineWidth: 10.0,
                      circularStrokeCap: CircularStrokeCap.round,
                      backgroundColor: const Color(0xff3B3B5A),
                      progressColor: Colors.orange[900],
                      center: Column(
                        crossAxisAlignment: CrossAxisAlignment.center,
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Text(
                            'remained',
                            style: AppStyles.subTitleTextStyle,
                          ),
                          Text(
                            '${consumerValue.getCurrentTimeRemained} sec',
                            style: AppStyles.head1TextStyle,
                          )
                        ],
                      ),
                    );
                  }),
                  SizedBox(
                    height: 30.h,
                  ),
                  Text(
                    'You will receive a notification when everything is ready!',
                    style: AppStyles.subTitleTextStyle,
                    textAlign: TextAlign.center,
                  )
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
