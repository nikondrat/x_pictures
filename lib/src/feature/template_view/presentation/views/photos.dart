import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:svg_flutter/svg.dart';
import 'package:x_pictures/src/core/constant/icons.dart';
import 'package:x_pictures/src/core/constant/styles.dart';
import 'package:x_pictures/src/data.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';

class PhotosView extends StatefulWidget {
  final List<ImageModel> models;
  const PhotosView({super.key, required this.models});

  @override
  State<PhotosView> createState() => _PhotosViewState();
}

class _PhotosViewState extends State<PhotosView> {
  Future<void> _showCustomDialog(String url) async {
    return showDialog<void>(
        context: context,
        barrierDismissible: true,
        builder: (BuildContext context) {
          return PopupImage(
            url: url,
            isProfile: false,
          );
        });
  }

  @override
  Widget build(BuildContext context) {
    var size = MediaQuery.of(context).size;

    /*24 is for notification bar on Android*/
    final double itemHeight = (size.height - kToolbarHeight - 24) / 2.5;
    final double itemWidth = size.width / 2;

    return Scaffold(
      appBar: AppBar(
        leading: CustomBackButton(
          onTap: () {
            router.goNamed(AppViews.homePageRoute);
          },
        ),
        title: Text(t.photos.title),
        actions: <Widget>[
          TextButton(
              onPressed: () {},
              child: Text(
                t.photos.save_all,
                style: TextStyle(color: Colors.white),
              ))
        ],
      ),
      body: SingleChildScrollView(
        child: Padding(
          padding: EdgeInsets.symmetric(horizontal: 15.w, vertical: 15.h),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                t.photos.save_all,
                style: AppStyles.subTitleTextStyle.copyWith(
                  fontSize: 10.sp,
                ),
              ),
              SizedBox(
                height: 5.h,
              ),
              Text(
                t.photos.photos_ready,
                style: AppStyles.head1TextStyle,
              ),
              SizedBox(
                height: 5.h,
              ),
              Text(
                t.photos.account,
                style: AppStyles.subTitleTextStyle.copyWith(
                  fontSize: 17.sp,
                ),
              ),
              SizedBox(
                height: 10.h,
              ),
              SizedBox(
                height: MediaQuery.of(context).size.height / 1.5,
                child: GridView.count(
                  physics: const NeverScrollableScrollPhysics(),
                  scrollDirection: Axis.vertical,
                  shrinkWrap: true,
                  crossAxisSpacing: 6,
                  mainAxisSpacing: 6,
                  crossAxisCount: 3,
                  childAspectRatio: (itemWidth / itemHeight),
                  children: widget.models.map((e) {
                    return GestureDetector(
                      onTap: () => _showCustomDialog(e.url),
                      child: Container(
                        decoration: BoxDecoration(
                          borderRadius:
                              BorderRadius.circular(AppValues.kRadius),
                          image: DecorationImage(
                              image: CachedNetworkImageProvider(e.url),
                              fit: BoxFit.cover),
                        ),
                        child: Align(
                          alignment: Alignment(0.9, -0.9),
                          child: Container(
                            width: 18.h,
                            height: 18.h,
                            child: GestureDetector(
                              child: SvgPicture.asset(
                                AppIcons.downloadGreyCircle,
                              ),
                            ),
                          ),
                        ),
                      ),
                    );
                  }).toList(),
                ),
              )
            ],
          ),
        ),
      ),
    );
  }
}
